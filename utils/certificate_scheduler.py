import schedule
import time
import threading
from flask import current_app
from services.certificate_service import CertificateService


class CertificateScheduler:
    """Scheduler para processar certificados automaticamente"""

    def __init__(self, app=None):
        self.app = app
        self._running = False
        self._thread = None
        self._initialized = False

    def init_app(self, app):
        """Inicializa o scheduler com a aplicação Flask"""
        if self._initialized:
            app.logger.warning(
                "Certificate scheduler já foi inicializado, ignorando...")
            return

        self.app = app
        self._initialized = True
        app.logger.info("Inicializando certificate scheduler...")
        self.start_scheduler()

    def _job_wrapper(self):
        """Wrapper para executar jobs dentro do contexto da aplicação"""
        with self.app.app_context():
            try:
                current_app.logger.info("Executando processamento de certificados...")
                CertificateService.process_completed_events()
                current_app.logger.info("Processamento de certificados concluído")
            except Exception as e:
                current_app.logger.error(
                    f"Erro no processamento de certificados: {str(e)}")

    def start_scheduler(self):
        """Inicia o scheduler em thread separada"""
        if self._running:
            self.app.logger.warning("Scheduler já está rodando, ignorando...")
            return

        # Limpar jobs existentes para evitar duplicação
        schedule.clear()

        # Agendar para executar a cada 6 horas
        schedule.every(6).hours.do(self._job_wrapper)

        # Testes
        # schedule.every(1).minutes.do(self._job_wrapper)

        # Também executar diariamente às 23:00
        schedule.every().day.at("23:00").do(self._job_wrapper)

        self.app.logger.info(f"Scheduler configurado com {len(schedule.jobs)} jobs")

        self._running = True
        self._thread = threading.Thread(target=self._run_schedule, daemon=True)
        self._thread.start()

        self.app.logger.info("Thread do scheduler iniciada")

    def _run_schedule(self):
        """Loop principal do scheduler"""
        while self._running:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto

    def stop_scheduler(self):
        """Para o scheduler"""
        self._running = False
        if self._thread:
            self._thread.join()


certificate_scheduler = CertificateScheduler()


def init_certificate_scheduler(app):
    """Função para inicializar o scheduler"""
    certificate_scheduler.init_app(app)
