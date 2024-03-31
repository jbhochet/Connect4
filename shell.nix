{ pkgs ? import <nixpkgs> { } }:

let
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
in

pkgs.mkShell {
  name = "Connect 4";

  packages = with pkgs; [
    (pythonPackages.python.withPackages (ps: with ps; [
      pip
      black
      snakeviz
      colorama
      matplotlib
    ]))
  ];
}
