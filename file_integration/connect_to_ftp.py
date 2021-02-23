import os
from ftplib import FTP
from django.conf import settings


def connect_ftp(path_server, path_ftp, file):
    ftp = FTP(settings.BERARD_FTP_HOST)
    ftp.login(settings.BERARD_FTP_USER, settings.BERARD_FTP_PWD)
    try:
        ftp.cwd(path_ftp)
        ftp.retrbinary(f'RETR {file}', open(os.path.join(path_server, file), 'wb').write)
        ftp.quit()
        return True
        # except Exception:
        #     ftp.cwd('/Rep__/EXPORT')
        #     ftp.retrbinary('RETR TART.PLN', open(os.path.join(paths, 'TART.PLN'), 'wb').write)
        #     ftp.quit()
        #     return True
    except Exception as e:
        print('error ftp', e)
        raise e
