import typing

from app.store.crm.accessor import CrmAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_accessors(app: 'Application'):
    app.crmaccessor = CrmAccessor()
    app.on_startup.append(app.crmaccessor.connect)
    app.on_cleanup.append(app.crmaccessor.disconnect)
