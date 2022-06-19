# Travel

A software manager for easy **development** and **distribution** of **Python code**.

The main features that Travel adds to Python are:

- Support for large-scale, **multi-package projects** (with common packages)
- **Reproducibility** (clear, transparent **dependency management**)
- Robust **development-lifecycle**, from prototyping to distribution
- Possibility to have different scoped Virtual Environment (e.g. for development, for testing, for notebooks...) with additional requirements

Travel is inspired by what **[Maven](https://maven.apache.org/)** is for Java and uses [Pip](https://github.com/pypa/pip) and [Virtual Environments](https://docs.python.org/3/library/venv.html).

## Why Travel

**Python is great** at many things, particularly for **scripting**. But it is powerful enough to create **complex software** too. Still, when doing so, it lacks some robustness and quickness.

Instead:

- Travel lets you **forget about repetitive setup of Python projects**, with creation of Virtual Environments, issues with imports, PYTHONPATH, folder structures. It does all of this for you.

- Travel ensures that when you run a Python script, all its **requirements are installed**. Along with reproducibility, this makes room for **easy collaboration** between developers.

- Also, while with standard tools it's hard to have multiple packages, one requiring another, with Travel this is a matter of **few YAML files**. You can **split your project** in several packages instead of having tons of requirements, code replication and/or single package-monoliths.

All in all, Travel lets you design **proper structure and modularity** for your code. No worries about imports and low-level stuff.

## Example of Travel Project

You can find an example of Travel project [here](https://github.com/travel-tools/travel/tree/master/src/travel/tests/data/complexproject).

## Installation

With Python >= 3.7 < 3.10, simply run

```
pip install travel
```

From now on, you can use `travel` from command line.


## Create a new project or add a new Bag

Travel supports several packages ("Bags") in a single project, nested in other folders ("Bags containing Bags"). You can create a project using [Travel Plans](https://github.com/travel-tools/cookiecutter-travelplan).

You can also create a new Bag after the first plan using `travel add`, to add a new [Travel Plan](https://github.com/travel-tools/cookiecutter-travelplan).

For a quick understanding, see below.

## Basic Usage

To see how to create your first Travel project, see the section above.

Once you have defined your structure of Bags (submodules of your project), for instance like in the [example](https://github.com/travel-tools/travel/tree/master/src/travel/tests/data/complexproject) or like this

```
complexproject/
    common/
        package/
        bag.yml
    microservices/
        first/
            package/
            bag.yml
        second/
            package/
            bag.yml
        bag.yml
    bag.yml
```

you can run

```
travel setup
```

in the main folder, where the first `bag.yml` file is located.

This will:

- Understand the dependencies
- Create the Virtual Environments
- Install the requirements
- Install the packages themselves in development mode (so that you can `import` them in their Virtual Environments)


You can also create a distribution package with `travel pack [commands]`, which is the equivalent of `python setup.py [commands]`, for instance:

```
travel pack sdist
```

in the folder of the Bag you want to pack. This will create the distribution in the `./build/package/dist` folder.

In any moment, you can run

```
travel clean
```

to destroy the Virtual Environments and other build objects.
