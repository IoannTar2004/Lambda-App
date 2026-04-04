import styles from "../../css/Function.module.css";
import {getStringDate} from "../../utils/formats.js";
import {deleteMetaFromName} from "../../utils/reserved.js";

const displayHeaders = {
  "id": "ID",
  "service": "Сервис",
  "environment": "Окружение",
  "handlerPath": "Путь к обработчику",
  "handler": "Обработчик",

  "bucket": "Бакет",
  "events": "События",
  "prefix": "Префикс",
  "suffix": "Суффикс"
}

const displayTexts = {
  "s3:ObjectCreated:Put": "Загрузить файл"
}

export const FunctionDescription = ({description}) => {
  const display = (name) => {
    if (typeof name === "object") {
      name = name.map(e => displayTexts[e] || e)
      name = name.join(", ")
      return name
    }

    return name
  }

  return (
      <div className={styles.functionDescription}>
        {Object.keys(displayHeaders).map(e => (
          <div className={styles.parameter}>
            <span className={styles.head}>{displayHeaders[e]}: </span>
            {display(deleteMetaFromName(e, description[e]))}
          </div>
        ))}
          <div className={styles.parameter}>
            <span className={styles.head}>Дата создания: </span>{getStringDate(description.createdAt)}
          </div>
          <div className={styles.parameter}>
            <span className={styles.head}>Размер памяти: </span>{description.memorySize} МБ
          </div>
          <div className={styles.parameter}>
            <span className={styles.head}>Таймаут: </span>{description.timeout} с
          </div>
        </div>
  )
}