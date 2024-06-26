{
  description = "Connect 4 flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-23.11";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = pkgs.lib;
        pythonPackages = pkgs.python3Packages;
        colorama = pythonPackages.buildPythonPackage rec {
          pname = "colorama";
          version = "0.4.6";
          format = "pyproject";
          doCheck = false;
          src = pkgs.fetchPypi {
            inherit pname version;
            sha256 = "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44";
          };
          nativeBuildInputs = with pythonPackages; [ hatchling ];
        };
        my-packages = with pythonPackages; [
          pip
          black
          snakeviz
          colorama
          matplotlib
          numpy
          pandas
        ];
        python-with-packages = pythonPackages.python.withPackages (ps: my-packages);
        my-packages-req = map (x: x.pname + "==" + x.version) my-packages;
      in
      {
        devShell = pkgs.mkShell {
          name = "Connect 4";

          packages = with pkgs; [
            python-with-packages
          ];

          shellHook = ''
            echo "${lib.concatStringsSep "\n" my-packages-req}" > requirements.txt
          '';
        };
      }
    );
}
