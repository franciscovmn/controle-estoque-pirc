# protocolo_aplicacao.py
import json

class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    class No:
        def __init__(self, produto):
            self.produto = produto
            self.esquerda = None
            self.direita = None

    def inserir(self, produto):
        if not self.raiz:
            self.raiz = self.No(produto)
        else:
            self._inserir(self.raiz, produto)

    def _inserir(self, no, produto):
        if produto.id < no.produto.id:
            if no.esquerda is None:
                no.esquerda = self.No(produto)
            else:
                self._inserir(no.esquerda, produto)
        else:
            if no.direita is None:
                no.direita = self.No(produto)
            else:
                self._inserir(no.direita, produto)

    def buscar(self, id):
        return self._buscar(self.raiz, id)

    def _buscar(self, no, id):
        if no is None or no.produto.id == id:
            return no
        if id < no.produto.id:
            return self._buscar(no.esquerda, id)
        return self._buscar(no.direita, id)

    def remover(self, id):
        self.raiz = self._remover(self.raiz, id)

    def _remover(self, no, id):
        if no is None:
            return no
        if id < no.produto.id:
            no.esquerda = self._remover(no.esquerda, id)
        elif id > no.produto.id:
            no.direita = self._remover(no.direita, id)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            temp = self._minimo(no.direita)
            no.produto = temp.produto
            no.direita = self._remover(no.direita, temp.produto.id)
        return no

    def _minimo(self, no):
        while no.esquerda:
            no = no.esquerda
        return no
