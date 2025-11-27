# setup.py

from setuptools import setup, find_packages

setup(
    name="git-quicklog",
    version="1.0.0",
    description="Un visualizzatore di log Git con avanzato con interfaccia CLI colorata",
    author="Salvatore Gerbino",
    author_email="salvatore.gerbino@edu-its.it",
    # Trova in maniera automatica  'quicklog' come package
    packages=["quicklog"],
    # Elenco delle dependeces che verrrano installate automaticamente
    install_requires=[
        "rich",
    ],
    # Creazione di un comando chiamato 'quicklog' che esegue la funzione 'run_app'
    # contenuto all'interno del file 'cli.py' nella cartella 'quicklog'
    entry_points={
        "console_scripts": [
            "quicklog = quicklog.cli:run_app",
        ],
    },
    python_requires=">=3.9",
)
