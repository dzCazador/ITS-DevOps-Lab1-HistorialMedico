from historial import __version__


def test_version_del_paquete_es_texto():
    assert isinstance(__version__, str)
    assert __version__ == "0.1.0"
