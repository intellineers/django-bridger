from django.apps import apps
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class FSMPreprocessor(Preprocessor):
    def __init__(self, *args, **kwargs):
        self.indicator = "!!!bridger-fsm"
        super().__init__(*args, **kwargs)

    def run(self, lines):
        for line in lines:
            if self.indicator in line:
                _, app_model, model_field = line.split(":")
                model = apps.get_model(app_model)

                yield "blockdiag {"

                transitions = getattr(model(), f"get_all_{model_field}_transitions")
                for transition in transitions():
                    yield f"\t{transition.source} -> {transition.target} [label='{transition.name}'];"

                yield "}"

            else:
                yield line


class FSMExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.register(FSMPreprocessor(), "bridger-fsm", 100)
