{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  name = "Connect 4";

  packages = with pkgs; [
    (python3.withPackages(ps: with ps; [
      black
    ]))
  ];
}
