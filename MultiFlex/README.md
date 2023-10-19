# README: MultiFlex
На входе - цепочка нормальных форм и теги
На выходе - составляющая в правильной форме
Написан на основе Морфосинтеза, см. описание тегов и проч. тут https://gitlab.mtsai.tk/ai/text-projects/lingTools/normalizer/-/blob/dev/MorphoGen/README.txt

## Запуск 
из Win:
.../normalizer set PYTHONPATH=.
.../normalizer python MultiFlex/multi_nums2wordforms_test.py --gram='Case=Dat' --lemma='десять красивый цветок' --test='MultiFlex/test_optional.txt' --debug='True'

из Ubuntu:
.../normalizer PYTHONPATH=. python3 MultiFlex/multi_nums2wordforms_test.py --gram='Case=Dat' --lemma='десять красивый цветок' --test='MultiFlex/test_optional.txt' --debug='True'


## Параметры:

--debug='True' -- прогон одного примера в консоли
--lemma='десять красивый цветок' - последовательность нормальных форм, которые надо склонять
--gram='Case=Dat;Gender=Fem' - форма, в которую надо поставить входную цепочку

Тесты:
--test='MultiFlex/test_optional.txt' - тест со сложными числительными, на данный момент покрыт на 0.88
--test='MultiFlex/test_obligatory.txt' - тест с числительными и/ли прилагательными, на данный момент покрыт на 1.0
