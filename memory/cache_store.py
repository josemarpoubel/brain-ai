"""
Cache Store

Compressed cache layer using CBOR2 for high-performance binary serialization.
"""

from typing import Dict, Any, Optional, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CacheStore:
    """
    Compressed cache layer using CBOR2 serialization.
    
    Features:
    - High-performance binary serialization
    - Temporary context storage
    - Reduced token usage for LLM interactions
    """
    
    def __init__(self, cache_path: str = "memory/cache"):
        """
        Initialize the Cache Store.
        
        Args:
            cache_path: Base directory for cache files
        """
        self.cache_path = Path(cache_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.in_memory_cache: Dict[str, Any] = {}
        logger.info(f"CacheStore initialized at {self.cache_path}")
    
    def write(self, key: str, value: Any, compress: bool = True) -> bool:
        """
        Write data to cache.
        
        Args:
            key: Unique identifier
            value: Data to cache
            compress: Whether to use CBOR compression
            
        Returns:
            True if write was successful
        """
        try:
            if compress:
                # Use CBOR for binary serialization
                import cbor2
                filename = f"{key.replace('/', '_')}.cbor"
                filepath = self.cache_path / filename
                
                with open(filepath, 'wb') as f:
                    cbor2.dump(value, f)
                
                logger.info(f"Cached (compressed): {key}")
            else:
                # Store in memory for fast access
                self.in_memory_cache[key] = value
                logger.info(f"Cached (memory): {key}")
            
            return True
        except ImportError:
            # Fallback to in-memory cache if CBOR not available
            self.in_memory_cache[key] = value
            logger.warning(f"CBOR not available, using in-memory cache: {key}")
            return True
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")
            return False
    
    def read(self, key: str, decompress: bool = True) -> Optional[Any]:
        """
        Read data from cache.
        
        Args:
            key: Unique identifier
            decompress: Whether to decompress CBOR data
            
        Returns:
            Cached data or None if not found
        """
        # Check in-memory cache first
        if key in self.in_memory_cache:
            logger.info(f"Cache hit (memory): {key}")
            return self.in_memory_cache[key]
        
        # Check file-based cache
        if decompress:
            filename = f"{key.replace('/', '_')}.cbor"
            filepath = self.cache_path / filename
            
            if filepath.exists():
                try:
                    import cbor2
                    with open(filepath, 'rb') as f:
                        data = cbor2.load(f)
                    logger.info(f"Cache hit (compressed): {key}")
                    return data
                except ImportError:
                    logger.warning("CBOR not available for decompression")
                    return None
                except Exception as e:
                    logger.error(f"Error reading cache: {e}")
                    return None
        
        logger.warning(f"Cache miss: {key}")
        return None
    
    def delete(self, key: str) -> bool:
        """
        Delete data from cache.
        
        Args:
            key: Unique identifier
            
        Returns:
            True if deletion was successful
        """
        # Remove from in-memory cache
        if key in self.in_memory_cache:
            del self.in_memory_cache[key]
        
        # Remove from file-based cache
        filename = f"{key.replace('/', '_')}.cbor"
        filepath = self.cache_path / filename
        
        if filepath.exists():
            filepath.unlink()
            logger.info(f"Cache entry deleted: {key}")
            return True
        
        logger.warning(f"Cache entry not found: {key}")
        return False
    
    def clear(self) -> int:
        """
        Clear all cached data.
        
        Returns:
            Number of entries cleared
        """
        count = 0
        
        # Clear in-memory cache
        count += len(self.in_memory_cache)
        self.in_memory_cache.clear()
        
        # Clear file-based cache
        for filepath in self.cache_path.glob("*.cbor"):
            filepath.unlink()
            count += 1
        
        logger.info(f"Cache cleared: {count} entries")
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary containing cache statistics
        """
        # Count file-based cache entries
        file_count = len(list(self.cache_path.glob("*.cbor")))
        
        # Calculate approximate size
        total_size = sum(
            f.stat().st_size for f in self.cache_path.glob("*.cbor") if f.is_file()
        )
        
        return {
            "cache_path": str(self.cache_path),
            "memory_entries": len(self.in_memory_cache),
            "file_entries": file_count,
            "total_size_bytes": total_size,
            "status": "active"
        }
    
    def get_ttl_keys(self, max_age_seconds: int) -> List[str]:
        """
        Get keys older than specified age (for TTL implementation).
        
        Args:
            max_age_seconds: Maximum age in seconds
            
        Returns:
            List of keys that should be expired
        """
        import time
        current_time = time.time()
        expired_keys = []
        
        for filepath in self.cache_path.glob("*.cbor"):
            if current_time - filepath.stat().st_mtime > max_age_seconds:
                key = filepath.stem.replace('_', '/')
                expired_keys.append(key)
        
        return expired_keys
    
    def cleanup_expired(self, max_age_seconds: int) -> int:
        """
        Remove expired cache entries.
        
        Args:
            max_age_seconds: Maximum age in seconds
            
        Returns:
            Number of entries removed
        """
        expired_keys = self.get_ttl_keys(max_age_seconds)
        
        for key in expired_keys:
            self.delete(key)
        
        logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        return len(expired_keys)
