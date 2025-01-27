from api.config.postgres import SessionLocal
from api.models.dto.paper import PaperDTO, PaperToUpdateDTO
from api.models.paper import Paper
from api.ports.paper import PaperRepository


class PaperAdapter(PaperRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_paper(self, paper: PaperDTO) -> Paper:
        paper_data = Paper(
            pdf_id=paper.pdf_id,
            area=paper.area,
            title=paper.title,
            authors=paper.authors,
            is_ignored=paper.is_ignored,
            total_pages=paper.total_pages,
            event_id=paper.event_id,
        )

        self._session.add(paper_data)
        self._session.commit()
        self._session.refresh(paper_data)

        return paper_data

    def get_papers(self, page: int = 1, page_size: int = 10) -> list[Paper]:
        papers = (
            self._session.query(Paper)
            .order_by(Paper.title)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

        return papers

    def get_papers_by_area(self, area: str) -> list[Paper]:
        return (
            self._session.query(Paper)
            .filter(Paper.area == area)
            .order_by(Paper.title)
            .all()
        )

    def get_paper_by_pdf_id(self, pdf_id: str) -> Paper:
        return self._session.query(Paper).filter(Paper.pdf_id == pdf_id).first()

    def get_first_paper(self) -> Paper:
        return self._session.query(Paper).first()

    def count_papers(self) -> int:
        return self._session.query(Paper).count()

    def count_papers_by_event_id(self, event_id: int) -> int:
        return self._session.query(Paper).filter(Paper.event_id == event_id).count()

    def get_areas_by_event_id(self, event_id: int) -> list[str]:
        areas = (
            self._session.query(Paper.area)
            .filter(Paper.event_id == event_id)
            .distinct()
            .all()
        )

        return [area[0] for area in areas]

    def update_paper(self, pdf_id: int, paper: PaperToUpdateDTO) -> Paper:
        paper_data = self._session.query(Paper).filter(Paper.pdf_id == pdf_id).first()

        paper_data.area = paper.area
        paper_data.title = paper.title
        paper_data.authors = paper.authors
        paper_data.is_ignored = paper.is_ignored

        self._session.commit()
        self._session.refresh(paper_data)

        return paper_data
