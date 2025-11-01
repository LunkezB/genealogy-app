from app.api.dependencies import get_db
from app.db.models import Person
from app.domain.sosa import generation_from_sosa, validate_sex_vs_sosa
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

router = APIRouter(prefix="/persons", tags=["persons"])


@router.put("/{sosa}", response_model=PersonOut)
def upsert_person(sosa: int, payload: PersonCreate, db: Session = Depends(get_db)):
    if sosa != payload.sosa:
        raise HTTPException(status_code=400, detail="Path sosa != payload.sosa")
    if not validate_sex_vs_sosa(payload.sex, payload.sosa):
        raise HTTPException(status_code=422, detail="Sex parity mismatch for sosa")

    if payload.birth and payload.death and payload.death < payload.birth:
        raise HTTPException(status_code=422, detail="death date earlier than birth date")

    obj = db.get(Person, payload.sosa)
    if obj is None:
        obj = Person(
            sosa=payload.sosa,
            sex=payload.sex,
            full_name=payload.full_name,
            birth=payload.birth,
            death=payload.death,
            place=payload.place,
            description=payload.description,
        )
        db.add(obj)
    else:
        obj.sex = payload.sex
        obj.full_name = payload.full_name
        obj.birth = payload.birth
        obj.death = payload.death
        obj.place = payload.place
        obj.description = payload.description
    db.commit()
    db.refresh(obj)

    return PersonOut(
        sosa=obj.sosa,
        sex=obj.sex,
        full_name=obj.full_name,
        birth=obj.birth,
        death=obj.death,
        place=obj.place,
        description=obj.description,
        generation=generation_from_sosa(obj.sosa),
    )


@router.get("/{sosa}", response_model=PersonOut)
def get_person(sosa: int, db: Session = Depends(get_db)):
    obj = db.get(Person, sosa)
    if obj is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return PersonOut(
        sosa=obj.sosa,
        sex=obj.sex,
        full_name=obj.full_name,
        birth=obj.birth,
        death=obj.death,
        place=obj.place,
        description=obj.description,
        generation=generation_from_sosa(obj.sosa),
    )


@router.patch("/{sosa}", response_model=PersonOut)
def patch_person(sosa: int, payload: PersonUpdate, db: Session = Depends(get_db)):
    obj = db.get(Person, sosa)
    if obj is None:
        raise HTTPException(status_code=404, detail="Person not found")

    if payload.sex is not None:
        if not validate_sex_vs_sosa(payload.sex, sosa):
            raise HTTPException(status_code=422, detail="Sex parity mismatch for sosa")
        obj.sex = payload.sex
    if payload.full_name is not None:
        obj.full_name = payload.full_name
    if payload.birth is not None:
        obj.birth = payload.birth
    if payload.death is not None:
        obj.death = payload.death
    if payload.place is not None:
        obj.place = payload.place
    if payload.description is not None:
        obj.description = payload.description

    if obj.birth and obj.death and obj.death < obj.birth:
        raise HTTPException(status_code=422, detail="death date earlier than birth date")

    db.commit()
    db.refresh(obj)
    return PersonOut(
        sosa=obj.sosa,
        sex=obj.sex,
        full_name=obj.full_name,
        birth=obj.birth,
        death=obj.death,
        place=obj.place,
        description=obj.description,
        generation=generation_from_sosa(obj.sosa),
    )


@router.get("", response_model=list[PersonOut])
def list_persons(
        generation: int | None = Query(default=None, ge=1),
        q: str | None = None,
        db: Session = Depends(get_db),
):
    stmt = select(Person)
    if q:
        like = f"%{q}%"
        stmt = stmt.filter(or_(Person.full_name.ilike(like), Person.place.ilike(like)))
    rows = db.execute(stmt).scalars().all()

    result: list[PersonOut] = []
    for p in rows:
        g = generation_from_sosa(p.sosa)
        if generation is None or generation == g:
            result.append(
                PersonOut(
                    sosa=p.sosa,
                    sex=p.sex,
                    full_name=p.full_name,
                    birth=p.birth,
                    death=p.death,
                    place=p.place,
                    description=p.description,
                    generation=g,
                )
            )
    result.sort(key=lambda r: r.sosa)
    return result


@router.delete("/{sosa}", status_code=204)
def delete_person(sosa: int, db: Session = Depends(get_db)):
    obj = db.get(Person, sosa)
    if obj is None:
        return
    db.delete(obj)
    db.commit()
