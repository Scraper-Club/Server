from core.models import ScrapComplainModel


class Complain(ScrapComplainModel):
    class Meta:
        proxy = True

    def get_url(self):
        if self.scrap:
            return self.scrap.url_value
        else:
            return 'Scrap was removed'

    def get_receiver(self):
        receiver = 'User: '
        if self.on_user:
            receiver += str(self.on_user)
        else:
            receiver += 'removed'

        receiver += ' Device: '

        if self.on_device:
            receiver += str(self.on_device)
        else:
            receiver += 'removed'

        receiver += ' IP: '
        if self.on_ip_address:
            receiver += str(self.on_ip_address)
        else:
            receiver += 'removed'

        return receiver

    def get_sender(self):
        if self.from_user:
            return str(self.from_user)
        else:
            'Sender was removed'
