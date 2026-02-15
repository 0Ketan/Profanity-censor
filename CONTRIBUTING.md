# Contributing to Profanity Censor

Thank you for your interest in contributing! We welcome contributions from the community.

## 🚀 How to Contribute

### 1. Fork the Repository

Click the "Fork" button at the top right of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/profanity-censor.git
cd profanity-censor
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

Follow these guidelines:

#### Code Style
- Use Python 3.8+
- Follow PEP 8 style guide
- Add docstrings for functions and classes
- Keep lines under 88 characters

#### Testing
- Test with both CPU and GPU if possible
- Test with various audio/video formats
- Include edge cases (empty files, long videos)

#### Documentation
- Update README.md if needed
- Add comments for complex logic
- Update changelog for new features

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add amazing new feature"
```

We use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `chore:` for maintenance

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

Go to the original repository and create a Pull Request. Please include:
- Clear description of changes
- Related issue numbers (if any)
- Screenshots or demos (if applicable)
- Testing steps

## 🎁 What Can You Contribute?

### Features
- [ ] Real-time microphone censorship
- [ ] Web interface
- [ ] Live streaming support
- [ ] Cloud processing
- [ ] Multiple voice detection

### Improvements
- [ ] Better accuracy with context awareness
- [ ] Custom beep patterns
- [ ] Whisper model fine-tuning
- [ ] Parallel batch processing

### Bugs
Check the [Issues](https://github.com/KetanSon/profanity-censor/issues) tab for bug reports.

### Documentation
- Language translations
- Video tutorials
- Blog posts
- Case studies

## 🔍 Pull Request Checklist

Before submitting a PR, please ensure:

- [ ] Code follows PEP 8 style guidelines
- [ ] Added/updated tests for new features
- [ ] All existing tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

## 🧪 Testing

To test your changes:

```bash
# Install in development mode
pip install -e .

# Test with sample files
python3 profanity_censor.py examples/sample.mp4
```

## 📝 Feature Suggestions

Have an idea? Create an [Issue](https://github.com/KetanSon/profanity-censor/issues) with:
- Clear feature description
- Use case examples
- Benefit to users

## 🐛 Bug Reports

When reporting bugs, please include:
- Your operating system
- Python version
- Error messages
- Steps to reproduce
- Sample file (if possible)

## ❓ Questions?

Feel free to:
- Create an Issue with `question` label
- Start a Discussion
- Reach out on LinkedIn/Twitter

## 📜 Code of Conduct

We pledge to make participation a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity.

## 📧 Contact

- Issues: [GitHub Issues](https://github.com/KetanSon/profanity-censor/issues)
- Discussions: [GitHub Discussions](https://github.com/KetanSon/profanity-censor/discussions)
- Twitter: [@yourhandle](https://twitter.com/yourhandle)
- LinkedIn: [Your Name](https://linkedin.com/in/yourname)

Thank you for contributing! 🎉

---

<p align="center">
  <i>Every contribution makes this project better! ❤️</i>
</p>
