# barter-lang
BarterLang - язык общего назначения, который компилируется под стековую виртуальную машину под C++.
Если вам проще учиться на примерах, проверьте папку 'src/test'
## Структура программы
Программа состоит из объявления функций. Программа обязательно должна содержать функцию "main" c возвращаемым типом void и пустым списком аргументов. Пример функции: 
```c++
func sum (int x int y) int {
  // dosomething
  return sum(x,y)
}
func main () void {
  // dosomething
  return 
}
```
Комментарии начинаются с "//". 
Будьте внимательны!
Команды внутри функции не разделяются точкой с запятой.
Аргументы внутри функции не разделяются запятой.
Вызов функций не должен содержать пробелов
В объявлении функции пробел между именем функции и списком аргументов обязателен.
Пробел перед открывающей скобкой { также обязателен.
Функции с типом данных void должны явно содержать инструкцию "return".
## Встроенные функции
```c++
sum (int x int y) int
mul (int x int y) int
div (int x int y) int
dif (int x int y) int
cou t(int x) void
```
## Переменные и типы данных
На данный момент существует два типа данных: int и bool. bool принимает только два значения true и false
```c++
  int five = 5
  bool flag = true
```
## Ссылки
Операции со ссылками могут быть небезопасными.
Ссылки хранятся в типе данных int.
```c++
func pass_ref (int x) void {
    cout(x)
    return
}
func main () void {
    int y = 18
    int z = 26
    int ptr = ref(y) //keep address of y
    cout(deref(ptr)) // prints 18
    pass_ref(ptr) // prints adress of y -> 0
    cout(deref(sum(ptr,1)))  // deref is not not safe! prints 26
    return
}
```
## Массивы
Тип данных в массиве всегда int.
```c++
  int arr = dec_arr(3) // declare array of the size 3
  cout(arr) // arr keeps a reference to the beggining of the array 
  cout(deref(sum(arr,1)))  // indexing array
  cout(deref(sum(arr,8))  // deref is not not safe again!
```
Без явной инициализации значений массива они могут быть любыми. Всегда явно инициализируйте массив!
## Запуск кода
Вы можете скачать скомпилированный бинарник, либо же использовать python для запуска кода.
Предпочитаемый способ - добавить компилятор в PATH.
Обязательной зависимостью в обоих вариантах является g++. 
```
barter run filename.barter  # Обыкновенный запуск программы
barter build filename.barter  # Только компиляция в папку build
barter run filename.barter -o # Запуск программы и сохранение файлов билда (.cpp, .exe) в папке build
barter run filename.barter -t # Запуск программы и вывод информации о времени компиляции и исполнения
```
Если запускаете с помощью python, вам понадобится версия 3.6+ (из-за использования f-string). 
Установка зависимостей и запуск кода:
```
pip install anytree
pip install argh
py barter.py run filename.barter
```