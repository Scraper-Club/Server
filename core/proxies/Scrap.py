from core.models import ScrapModel, ScrapComplainModel
from core.proxies import Device


class Scrap(ScrapModel):
    class Meta:
        proxy = True

    def get_result_bytes(self, encoding=None):
        if encoding:
            return self.file.tobytes(encoding)
        else:
            return self.file.tobytes()

    def get_result_str(self, encoding='utf-8'):
        return self.file.tobytes().decode(encoding)

    def on_complained(self):
        ScrapComplainModel.objects.create(
            scrap=self,
            from_user=self.owner,
            on_device=self.scraper_device,
            on_user=self.scraper_user,
            on_ip_address=self.ip_address,
        )
        self.scraper_user.scraper.add_complain()
        #TODO refactor device add complain logic
        device = Device.objects.get(device_id=self.scraper_device.device_id)
        device.add_complain()
        self.complained = True
        self.save()

    def get_file_size(self):
        return len(self.file)

    def can_complain(self):
        return not self.complained and self.scraper_user and self.scraper_device and self.ip_address