# Brain-AI

![Brain-AI Logo](https://drive.google.com/file/d/1Ngd9T72qoEDHnz_sJdPe0u5TE-01rxbq/view/brain-ai.png)

## Description

**Brain-AI** is an innovative project aimed at creating an "efficient brain" for artificial intelligence systems. It integrates tools such as **Obsidian**, **SQLite3**, and **Cbor2** to optimize context management, reduce token consumption, and minimize hallucinations in LLMs (Large Language Models), whether online or local. The goal is to provide a solid foundation for daily use journeys, allowing AI to maintain consistency and efficiency across diverse contexts without overburdening computational resources.

This repository serves as a starting point for developers interested in improving interactions with LLMs, focusing on efficient data storage, fast information retrieval, and seamless integration between productivity tools and lightweight databases.

## Main Features

- **Obsidian Integration**: Utilizes the power of Obsidian to create and manage interconnected knowledge bases, allowing AI to navigate notes and contexts intuitively.
- **SQLite3 Storage**: Lightweight and efficient database for storing structured data, reducing latency and optimizing access to historical information.
- **CBOR2 Serialization**: Employs CBOR (Concise Binary Object Representation) for data compression and serialization, minimizing the use of tokens in interactions with LLMs and accelerating processing.
- **Support for Online and Local LLMs**: Compatible with models such as GPT, Llama, or others, ensuring that AI avoids confusion between different contexts, promoting more accurate and contextually relevant responses.
- **Hallucination Reduction**: Algorithms designed to filter and prioritize relevant information, avoiding unwanted digressions in conversations or tasks.

## Technologies Used

- **Obsidian**: For knowledge management and interconnected notes.
- **SQLite3**: Lightweight relational database for persistent storage.
- **Cbor2**: Library for efficient binary serialization.
- **Python** (or other languages as per implementation): Main language for development.
- **LLM APIs**: Integration with services such as OpenAI, Hugging Face, or local models via Ollama.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/josemarpoubel/brain-ai.git
   cd brain-ai
   ```

2. Install the dependencies (example with Python):
   ```bash
   pip install -r requirements.txt
   ```
   Make sure Obsidian is installed and configured on your system.

3. Configure the SQLite3 database:
   - Run the initialization script to create the database:
     ```bash
     python setup_db.py
     ```

4. For integration with local LLMs, install tools like Ollama or similar.

## Usage

1. **Initial Setup**:
   - Import your notes from Obsidian into the system.
   - Configure credentials for online LLMs (if applicable).

2. **Basic Execution**:
   - Run the main script:
     ```bash
     python brain_ai.py --query "Your question here"
     ```
   - The system will query the database, serialize data with CBOR, and interact with the LLM to generate optimized responses.

3. **Integration Example**:
   - To avoid hallucinations: Brain-AI filters relevant contexts before sending prompts to the LLM, reducing unnecessary tokens.

For more details, consult the internal documentation or the examples in the `examples/` directory.

## Contribution

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a branch for your feature: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -m 'Adds new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a Pull Request.

Please follow the code guidelines and include tests for new features.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.

## Roadmap

- [ ] Advanced support for multiple LLMs.
- [ ] Web interface for context management.
- [ ] Optimizations for mobile devices.
- [ ] Integration with additional tools such as Notion or Roam Research.

## Contact

- **Author**: Josemar Poubel
- **Email**: josemarpoubel@msn.com
- **GitHub**: [Josemar Poubel](https://github.com/josemarpoubel)

For questions or suggestions, please open an issue in the repository.

---

*Last updated: Sunday, April 19, 2026*
