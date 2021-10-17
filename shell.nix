# Run nix-shell without arguments to enter an environment with all the
# project dependencies in place.
{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "nixos-21.05";
  }) {}
}:

pkgs.mkShell {
  venvDir = "./.venv";
  buildInputs = with pkgs; [
    python38
    python38Packages.venvShellHook
    python39
    python310
  ];
  postShellHook = ''
    unset SOURCE_DATE_EPOCH

    # Install dev requirements
    pip install -e .\[dev,dist\]
  '';
}
