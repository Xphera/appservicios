import hashlib


class CodeFactoryUtil():

        BUFFER_BYTES_CODIGO_VALIDACION = 3 #3 BYTES = 24 BITS = 6 LETRAS

        @staticmethod
        def codigoValidacionEmail(email):
            byte_email = email.encode()
            h = hashlib.new("shake_128")
            h.update(byte_email)
            return h.hexdigest(CodeFactoryUtil.BUFFER_BYTES_CODIGO_VALIDACION)

        @staticmethod
        def verificarCodigoValidacionEmail(email,codigo):
            codigo_gen = CodeFactoryUtil.codigoValidacionEmail(email)
            return codigo_gen == codigo
