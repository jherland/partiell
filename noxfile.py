from glob import glob
import nox

# Run everything but 'dist' by default
nox.options.keywords = "not dist"


@nox.session(python=["3.8", "3.9", "3.10"], reuse_venv=True)
def test(session):
    session.install("-e", ".")
    session.run("python", "-m", "doctest", *glob("src/*.py"))
    session.run("python", "-m", "unittest", "discover", *session.posargs)


@nox.session(reuse_venv=True)
def format(session):
    session.install("-e", ".[dev]")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-e", ".[dev]")
    session.run("flake8")


@nox.session(reuse_venv=True)
def dist(session):
    session.install("-e", ".[dist]")
    session.run("check-manifest")
    session.run("python", "setup.py", "bdist_wheel", "sdist")
    session.run("twine", "upload", *glob("dist/*"))
    print("*** Don't forget to tag and push!")
