from src.models.service import Service
from src.models.category import Category
from src.models.master import Master


hair_care = Category(name='Уход за волосами', id=1)
nail_care = Category(name='Уход за ногтями', id=2)
massage_spa = Category(name='Массаж, SPA', id=3)
skin_care = Category(name='Уход за кожей', id=4)
tattoos = Category(name='Татуировки', id=5)
piercing = Category(name='Пирсинг', id=6)
hair_care_services = [Service(name='Стрижка', category=hair_care), Service(name='Окрашивание', category=hair_care),
                      Service(name='Мелирование', category=hair_care), Service(name='Укладка', category=hair_care)]
nail_care_services = [Service(name='Маникюр', category=nail_care), Service(name='Педикюр', category=nail_care),
                      Service(name='Наращивание ногтей', category=nail_care)]
massage_spa_services = [Service(name='Массаж', category=massage_spa), Service(name='SPA', category=massage_spa),
                        Service(name='Тайский массаж', category=massage_spa)]
skin_care_services = [Service(name='Удаление прыщей', category=skin_care),
                      Service(name='Чистка кожи', category=skin_care)]
tattoos_services = [Service(name='Цветные татуировки', category=tattoos),
                    Service(name='Монохромные татуировки', category=tattoos),
                    Service(name='Удаление татуировок', category=tattoos)]
piercing_services = [Service(name='Пирсинг головы', category=piercing), Service(name='Пирсинг тела', category=piercing)]
all_categories = [hair_care, nail_care, massage_spa, skin_care, tattoos, piercing]
all_services = hair_care_services + nail_care_services + massage_spa_services + skin_care_services + tattoos_services + piercing_services


def test_search():
    master1 = Master(name='Ольга', surname='Иванова', services=[hair_care_services[1], nail_care_services[1], tattoos_services[0]])
    master2 = Master(name='Ольга', surname='Петрова', services=[tattoos_services[0]])
    master3 = Master(name='Екатерина', surname='Бородина', services=[hair_care_services[0], massage_spa_services[0], piercing_services[0]])
    masters = [master1, master2, master3]
    assert search(masters, 'Ольга') == [master1, master2]
    assert search(masters, 'ольга') == [master1, master2]
    assert search(masters, 'Иванова') == [master1]
    assert search(masters, 'иванова') == [master1]
    assert search(masters, 'Ольга Петрова') == [master2]
    assert search(masters, 'ольга петрова') == [master2]
    assert search(masters, 'Петрова Ольга') == [master2]
    assert search(masters, 'петрова ольга') == [master2]
    assert search(masters, 'петрова ольга') == [master2]
    assert search(masters, 'Окрашивание') == [master1]
    assert search(masters, 'окрашивание') == [master1]
    assert search(masters, 'Пирсинг') == [master3]
    assert search(masters, 'пирсинг') == [master3]
    assert search(masters, 'Цветные татуировки') == [master2, master3]
    assert search(masters, 'test') == []
    assert search(masters, 'Test Test') == []


def search(masters, query):
    result = []
    query = query.lower()
    # категория
    found_category = None
    for category in all_categories:
        if category.name.lower().find(query) != -1:
            found_category = category
            break
    if found_category:
        for m in masters:
            for s in m.services:
                if s.category == found_category:
                    result.append(m)
        return result
    # услуга
    found_service = None
    for service in all_services:
        if service.name.lower().find(query) != -1:
            found_service = service
            break
    if found_service:
        for m in masters:
            if found_service in m.services:
                result.append(m)
        return result
    # имя
    for m in masters:
        name = (m.name + ' ' + m.surname).lower()
        reverse_name = (m.surname + ' ' + m.name).lower()
        r = name.find(query)
        r2 = reverse_name.find(query)
        if r != -1 or r2 != -1:
            result.append(m)
    return result
