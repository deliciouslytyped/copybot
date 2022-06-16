#! /usr/bin/env -S nix-shell -I nixpkgs=channel:nixos-unstable
{pkgs ? import <nixpkgs> {}}: pkgs.mkShell {
  packages = with pkgs; [ poetry git sqlite sqlitebrowser ];
  shellHook = ''
    function dev {
      poetry shell
      }
    dev
    '';
  }
