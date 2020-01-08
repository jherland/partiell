# Run nix-shell without arguments to enter an environment with all the
# development dependencies in place.

with import <nixpkgs> {};

mkShell {
  name = "partiell-env";
  buildInputs = [
    (python38.withPackages (ps: with ps; [
      setuptools
      pip
      wheel
    ]))
    libffi
    gcc
  ];
  shellHook = ''
    # Setup up virtualenv for development
    python -m venv --clear .venv
    source .venv/bin/activate

    # Allow the use of wheels.
    unset SOURCE_DATE_EPOCH
    pip install wheel --disable-pip-version-check

    # Install dev requirements
	pip install -e .\[dev\]
  '';
}
