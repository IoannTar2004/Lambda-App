import styles from "../../css/Function.module.css"
import {useLocation} from "react-router";
export const EditPage = () => {

  const location = useLocation()
  const functionData = location.state.functionData

  return (
      <div className={styles.modalContent}>
        <div className={styles.formWindow}>
          <div className={styles.head}>Путь к обработчику</div>
          <input value={functionData.handlerPath}/>

          <div className={styles.head}>Обработчик</div>
          <input value={functionData.handler}/>

          <div className={styles.head}>Размер памяти</div>
          <select name="cars" id="cars">
            <option value="volvo">128 МБ</option>
            <option value="volvo">256 МБ</option>
            <option value="saab">512 МБ</option>
            <option value="mercedes">1024 МБ</option>
          </select>

          <div className={styles.head}>Таймаут (в секундах)</div>
          <input type={"number"} max={300} min={1} value={300}/>
          <div className={styles.saveParametersBox}>
            <button id={styles.saveParametersButton}>Сохранить</button>
          </div>
        </div>
      </div>
  )
}