"""Punto de entrada del sistema de historial médico."""

from historial.menu import Menu
from historial.repositorio import RepositorioHistorial


def main():
    """Crea el repositorio en memoria y ejecuta el menú de consola."""
    repositorio = RepositorioHistorial()
    Menu(repositorio).ejecutar()


if __name__ == "__main__":
    main()
