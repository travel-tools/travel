# Travel

A software manager for easy **development** and **distribution** of **Python code**.

The main features that Travel adds to Python are:

- Support for large-scale, **multi-package projects**
- **Reproducibility** (clear, transparent **dependency management**)
- Robust **development-lifecycle**, from blueprinting to distribution 

Travel is inspired by what **[Maven](https://maven.apache.org/)** is for Java and uses [Pip](https://github.com/pypa/pip) and [Virtual Environments](https://docs.python.org/3/library/venv.html).

## Why Travel

**Python is great** in many things, particularly for **scripting**. But it is powerful enough to create **complex software** too. Still, when doing so, it lacks some robustness and quickness.

Instead:
 
- Travel lets you **forget about repetitive setup of Python projects**, with creation of Virtual Environments, issues with imports, PYTHONPATH, folder structures. It does all of this for you.

- Travel ensures that when you run a Python script, all its **requirements are implicitly installed**. Along with reproducibility, this makes room for **easy collaboration** between developers.

- Also, while with standard tools it's hard to have multiple packages, one requiring the other, with Travel is a matter of **few YAML files**. You can **split your project** in several packages instead of having tons of requirements, code replication and/or single package-monoliths. 

All in all, Travel lets you design **proper structure and modularity** for your code. No worries about imports and low-level stuff.

## Example of Travel Project

You can find an example of Travel project [here](https://github.com/travel-tools/travel/tree/master/src/travel/tests/data/complexproject).