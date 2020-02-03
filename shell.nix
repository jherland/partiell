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
    unset SOURCE_DATE_EPOCH
    python -m venv --clear .venv
    source .venv/bin/activate

    # Install dev requirements
    pip install -e .\[dev\]
  '';
}
