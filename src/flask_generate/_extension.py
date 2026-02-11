from flask import Flask


class Generate:

    def __init__(self, app: Flask | None = None) -> None:
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if 'generate' in app.extensions:
            raise RuntimeError(
                'A Generate extension is already initialized on this application.'
            )
        app.extensions['generate'] = self