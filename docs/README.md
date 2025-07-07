# NDP EP Documentation

This directory contains the complete documentation for the ndp-ep Python client library, built with Sphinx.

## 📁 Structure

```
docs/
├── source/                     # Sphinx source files
│   ├── conf.py                # Sphinx configuration
│   ├── index.rst              # Main documentation page
│   ├── installation.rst       # Installation guide
│   ├── quickstart.rst         # Quick start guide
│   ├── authentication.rst     # Authentication guide
│   ├── api_reference.rst      # Complete API reference
│   ├── user_guide/           # Detailed user guides
│   │   ├── organizations.rst  # Working with organizations
│   │   ├── resources.rst      # Managing resources
│   │   ├── search.rst         # Search functionality
│   │   └── system_info.rst    # System information
│   ├── tutorials/            # Interactive tutorials
│   │   ├── getting_started.ipynb        # Main tutorial
│   │   ├── data_management_workflow.ipynb
│   │   └── advanced_search.ipynb
│   ├── _static/              # Static files (CSS, images)
│   └── _templates/           # Custom templates
├── build/                    # Generated documentation (gitignored)
├── requirements.txt          # Documentation dependencies
├── Makefile                 # Build commands
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Install documentation dependencies:**

   ```bash
   cd docs
   pip install -r requirements.txt
   ```

   Or using the Makefile:

   ```bash
   make install
   ```

2. **Build the documentation:**

   ```bash
   make html
   ```

3. **View the documentation:**

   ```bash
   make serve
   ```

   This will build the docs and open them in your default browser.

## 🔧 Building Documentation

### Available Make Targets

```bash
# Install dependencies
make install

# Build HTML documentation
make html

# Build and open in browser
make serve

# Clean build directory
make clean

# Live reload during development
make live
```

### Manual Build

If you prefer not to use Make:

```bash
# Install dependencies
pip install -r requirements.txt

# Build documentation
sphinx-build -M html source build

# Clean build
sphinx-build -M clean source build
```

## 📝 Writing Documentation

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory:
   - `source/` for main pages
   - `source/user_guide/` for user guides
   - `source/tutorials/` for tutorials

2. Add the file to the appropriate `toctree` directive in `index.rst` or parent page

3. Rebuild the documentation

### RST Syntax

The documentation uses reStructuredText (RST) format. Key syntax:

```rst
Page Title
==========

Section
-------

Subsection
~~~~~~~~~~

**Bold text**
*Italic text*
``Code text``

.. code-block:: python

   # Python code example
   from ndp_ep import APIClient
   client = APIClient(base_url="...")

.. note::
   This is a note box

.. warning::
   This is a warning box

`Link text <https://example.com>`_
```

### Code Examples

Always include working code examples:

```rst
.. code-block:: python

   from ndp_ep import APIClient

   # Initialize client
   client = APIClient(
       base_url="http://155.101.6.191:8003",
       token="your-token"
   )

   # List organizations
   organizations = client.list_organizations()
   print(f"Found {len(organizations)} organizations")
```

### API Documentation

API documentation is auto-generated from docstrings. To add new API documentation:

1. Ensure your Python code has proper docstrings
2. Add autoclass/automodule directives in `api_reference.rst`:

```rst
.. autoclass:: YourNewClass
   :members:
   :show-inheritance:
```

## 📓 Jupyter Notebooks

### Creating Tutorial Notebooks

1. Create notebooks in `source/tutorials/`
2. Include Colab and Binder badges at the top:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/your_notebook.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fyour_notebook.ipynb)
```

3. Test notebooks work in both Colab and Binder
4. Add notebook to `index.rst` toctree

### Notebook Guidelines

- Start with library installation: `!pip install ndp-ep`
- Include comprehensive examples and explanations
- Add error handling and troubleshooting
- Test with and without authentication
- Use markdown cells for explanations

## 🎨 Customization

### Theme Configuration

The documentation uses the Read the Docs theme. Customize in `source/conf.py`:

```python
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
```

### Custom CSS

Add custom styles in `source/_static/custom.css`:

```css
/* Custom styles */
.wy-nav-content {
    max-width: 1200px;
}

.highlight-python .highlight {
    background: #f8f8f8;
}
```

### Custom Templates

Override templates by creating files in `source/_templates/`:

- `layout.html` - Main layout
- `navigation.html` - Navigation menu
- `searchbox.html` - Search box

## 🚀 Deployment

### GitHub Pages

To deploy to GitHub Pages:

1. Build documentation: `make html`
2. Copy `build/html/*` to your gh-pages branch
3. Push to GitHub

### Read the Docs

1. Connect your GitHub repository to Read the Docs
2. Configure build settings:
   - Python version: 3.8+
   - Requirements file: `docs/requirements.txt`
   - Documentation type: Sphinx

### Manual Deployment

Deploy to any web server by uploading the `build/html/` directory.

## 🔍 Troubleshooting

### Common Issues

**"No module named 'ndp_ep'"**

Install the package in development mode:

```bash
pip install -e .
```

**"Extension error"**

Check that all Sphinx extensions are installed:

```bash
pip install -r docs/requirements.txt
```

**"Notebook execution failed"**

Notebooks are set to `nbsphinx_execute = 'never'` by default. To execute during build:

```python
# In conf.py
nbsphinx_execute = 'always'
```

**"Theme not found"**

Install the theme:

```bash
pip install sphinx-rtd-theme
```

### Build Debugging

Enable verbose output:

```bash
sphinx-build -v -M html source build
```

Check for warnings:

```bash
sphinx-build -W -M html source build
```

### Live Development

For continuous rebuilding during development:

```bash
pip install sphinx-autobuild
sphinx-autobuild source build/html --open-browser
```

## 🤝 Contributing

### Documentation Guidelines

1. **Clarity**: Write for beginners and experts alike
2. **Examples**: Include working code examples
3. **Testing**: Test all examples and links
4. **Consistency**: Use consistent formatting and style
5. **Updates**: Keep documentation in sync with code changes

### Review Process

1. Create documentation changes in a feature branch
2. Test builds locally: `make html`
3. Test notebooks in Colab/Binder
4. Submit PR with documentation changes
5. Ensure CI passes and documentation builds

### Style Guide

- Use present tense: "The client connects..." not "The client will connect..."
- Use active voice: "You can configure..." not "Configuration can be..."
- Use "you" to address the reader
- Keep sentences concise and clear
- Use code examples liberally
- Add screenshots for UI elements (if any)

## 📊 Analytics

### Tracking Documentation Usage

If you want to track documentation usage, add Google Analytics:

```python
# In conf.py
html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',  # Your GA4 tracking ID
}
```

### Feedback Collection

Consider adding feedback mechanisms:

- GitHub Issues for documentation bugs
- Discussion forums for questions
- Survey links for user feedback

## 🆘 Getting Help

If you need help with the documentation:

1. **Check existing issues**: [GitHub Issues](https://github.com/sci-ndp/ndp-ep-py/issues)
2. **Sphinx documentation**: [Sphinx Docs](https://www.sphinx-doc.org/)
3. **RST guide**: [RST Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
4. **RTD theme docs**: [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)

---

## 📄 License

This documentation is part of the ndp-ep project and is licensed under the MIT License.

---

*Last updated: 2025-01-06*