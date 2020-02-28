from mkautodoc.extension import MKAutoDocExtension, AutoDocProcessor


class DjangoAutoDocProcessor(AutoDocProcessor):
    def run(self, parent, blocks):
        try:
            super().run(parent, blocks)
        except:
            pass


class DjangoDocstringExtension(MKAutoDocExtension):
    def extendMarkdown(self, md):
        import django

        django.setup()

        md.registerExtension(self)
        processor = DjangoAutoDocProcessor(md.parser, md=md)
        md.parser.blockprocessors.register(processor, "mkautodoc", 110)


def makeExtension():
    return DjangoDocstringExtension()
