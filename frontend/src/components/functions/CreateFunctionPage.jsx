import styles from "../../css/Function.module.css"
import {Fragment, useEffect, useState} from "react";

export const CreateFunctionPage = () => {

  const [projectStructure, setProjectStructure] = useState([])
  const [functionSuggestions, setFunctionSuggestions] = useState([])

  useEffect(() => {
    setProjectStructure(["a/ab/f1.py", "a/ab/f2.py", "a/f1.py", "b/f1.py", "c/", "a1.js", "a2.py"])
  }, []);

  const handleOnBlurHandlerPath = (e) => {
    const handler = e.target.value
    const extension = handler.split(".").pop()

    if (handler !== "")
      setFunctionSuggestions(["f1", "f2", "f3"])
  }

  return (
      <div className={styles.content}>
        <div className={styles.newFunctionBox}>
          <h1>Новая функция</h1>
          <form>
            <label>Название </label>
            <input maxLength={64} minLength={3}/>

            <label>Cервис </label>
            <select>
              <option value={"S3"}>Хранилище S3</option>
            </select>

            <ServiceParameters service={"S3"} />

            <label>Путь к обработчику </label>
            <input maxLength={256} minLength={1} list={"handlers"} onBlur={handleOnBlurHandlerPath}/>
            <datalist id={"handlers"}>
              {projectStructure.filter(e => e[e.length - 1] !== "/")
                  .map(e => <option value={e} />)}
            </datalist>

            <label>Обработчик </label>
            <input maxLength={256} minLength={1} list={"functions"} />
            <datalist id={"functions"}>
              {functionSuggestions.map(e => <option value={e} />)}
            </datalist>

            <label>Размер памяти </label>
            <select>
              <option value={128}>128 МБ</option>
              <option value={256}>256 МБ</option>
              <option value={512}>512 МБ</option>
              <option value={1024}>1024 МБ</option>
            </select>

            <label>Таймаут (в секундах) </label>
            <input type={"number"} max={300} min={1} />

            <button type={"submit"}>Создать</button>
          </form>
        </div>
      </div>

  )
}

const ServiceParameters = ({service}) => {
  switch (service) {
    case "S3":
      return (
          <Fragment>
            <label className={styles.specialParameter}>Имя бакета </label>
            <input maxLength={64} minLength={3} />

            <label className={styles.specialParameter}>Событие S3 </label>
            <select>
              <option title="s3:ObjectCreated:Put" value={"S3"}>Загрузить объект</option>
              <option title="s3:ObjectRemoved:Delete" value={"S3"}>Удалить объект</option>
            </select>

            <label className={styles.specialParameter}>Префикс </label>
            <input maxLength={256} minLength={1} />

            <label className={styles.specialParameter}>Суффикс </label>
            <input maxLength={256} minLength={1} />

          </Fragment>
      )
  }
}