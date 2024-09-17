from utils.get_names_files import get_names_files, get_bairros
from utils.get_xslx import get_data
from utils.generator_maps import generate_map

def main ():
    arquivos_dp = get_names_files("src/DP-2023")
    bairros_dp = get_bairros(arquivos_dp)
    zip_bairros = zip(arquivos_dp, bairros_dp)
    data = get_data(zip_bairros)
    generate_map(data)


if __name__ == "__main__":
    main()