# This Python file uses the following encoding: utf-8
from tkinter import messagebox as mb


class Exceptions:
    @classmethod
    def ACCOUNT_NOT_FOUND(cls, line_number, guide_number):
        mb.showwarning('Erro', f'Linha da planilha:{line_number}\nConta: {guide_number} não foi encontrada na guia')

    @classmethod
    def PROCEDURE_NOT_FOUND(cls, line_number, procedure_code):
        message = f'Linha da planilha:{line_number}\nProcedimento: {procedure_code} não foi encontrada na guia'
        mb.showwarning('Erro', message)

