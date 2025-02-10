{
  description = "Development environment for interview bot";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    google-genai = pkgs.python312Packages.buildPythonPackage rec {
      pname = "google-genai";
      version = "1.0.0";
      format = "pyproject";

      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/2f/c3/fba38ba11a9b97b0a6ca6d46ec0dcd3c7bdf3ecf83eec6e6117ac25106c7/google_genai-1.0.0.tar.gz";
        sha256 = "sha256-FXEqu4CPiRoU6vye3yG4z5LqlS9ifdDi6Tllfv0jSs0=";
      };

      nativeBuildInputs = with pkgs.python312Packages; [
        setuptools
        wheel
      ];

      propagatedBuildInputs = with pkgs.python312Packages; [
        google-auth
        requests
        pydantic
        websockets
      ];

      doCheck = false;
    };
    pythonEnv = pkgs.python312.withPackages (ps:
      with ps; [
        transformers
        accelerate
        python-dotenv
        google-genai
      ]);
  in {
    formatter.${system} = nixpkgs.legacyPackages.x86_64-linux.alejandra;
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [
        pythonEnv
      ];
      shellHook = ''
        # Set Python environment
        export PYTHONPATH="${pythonEnv}/${pythonEnv.sitePackages}"
        echo "Development environment ready!"
      '';
    };
  };
}
