{
  description = "Доброе утро!";

  inputs = {
    pre-commit-hooks-nix.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs = inputs @ { nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.pre-commit-hooks-nix.flakeModule
      ];

      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem = { pkgs, config, ... }:
        let
          takeAttrs = attrList: x: (map (attr: x."${attr}") attrList);

          python = pkgs.python311;
          pythonDeps = [
            "pyrogram"
            "tgcrypto"
          ];
          pythonDevDeps = [
            "black"
            "mypy"
            "isort"
          ];
          devPython = python.withPackages (takeAttrs (pythonDeps ++ pythonDevDeps));
        in
        {
          packages.default =
            python.pkgs.buildPythonApplication {
              name = "goodmorninguserbot";
              format = "pyproject";
              buildInputs = with python.pkgs; [ setuptools ];
              propagatedBuildInputs = takeAttrs pythonDeps python.pkgs;
              src = ./.;
            };


          devShells.default =
            pkgs.mkShellNoCC {
              inherit (config.pre-commit.devShell) shellHook;
              packages = [ devPython ];
              env = {
                LOGLEVEL = "DEBUG";
              };
            };

          pre-commit.settings = {
            hooks = {
              black.enable = true;
              isort.enable = true;
              nixpkgs-fmt.enable = true;
              mypy.enable = true;
            };

            settings = {
              isort.profile = "black";
              mypy.binPath = "${devPython}/bin/mypy";
            };
          };

          formatter = pkgs.nixpkgs-fmt;
        };
    };
}
