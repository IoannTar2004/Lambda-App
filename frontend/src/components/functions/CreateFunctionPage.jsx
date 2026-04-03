import styles from "../../css/Function.module.css"
import {Fragment, useEffect, useRef, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {HttpStatusCode} from "axios";

export const CreateFunctionPage = () => {

  const {projectId} = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const [projectStructure, setProjectStructure] = useState([])
  const [functionSuggestions, setFunctionSuggestions] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [parameters, setParameters] = useState({timeout: 5})
  const [error, setError] = useState("")
  const [service, setService] = useState("")

  const runnableCache = useRef(new Map())

  useEffect(() => {
    if (location?.state?.projectStructure)
      setProjectStructure(location.state.projectStructure)
    else
      httpRequest(HTTPMethods.GET, "/api/code/user-files/listdir-all", {
        projectId: projectId,
        path: ""
      }).then((e) => {
          const project = e.data
          const getStructure = project.map(e => e.key.split("/").slice(2).join("/"))
          setProjectStructure(getStructure)
        })
  }, []);

  const handleOnFonusRuns = (e) => {
    const handlerPath = parameters.handlerPath
    if (!handlerPath) return

    if (runnableCache.current.has(handlerPath))
      setFunctionSuggestions(runnableCache.current.get(handlerPath))
    else if (projectStructure.includes(handlerPath))
      httpRequest(HTTPMethods.GET, "/api/code/user-files/runnable-list", {
        projectId: projectId,
        path: handlerPath
      }).then(e => {
        const runs = e.data
        runnableCache.current.set(handlerPath, runs)
        setFunctionSuggestions(runs)
      })
    else
      setFunctionSuggestions([])

    //
    // if (handler !== "")
    //   setFunctionSuggestions(["f1", "f2", "f3"])
  }

  const handleOnChange = (key, input) => {
    setError("")
    const newParameters = {...parameters}
    newParameters[key] = input
    setParameters(newParameters)
  }

  const handleCheckboxes = (key, input, checked) => {
    setError("")
    let arr = parameters[key] ? parameters[key] : []
    if (checked)
      arr.push(input)
    else
      arr = arr.filter(e => e !== input)

    const newParameters = {...parameters}
    newParameters[key] = arr
    setParameters(newParameters)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const requestParameters = {...parameters, projectId: projectId}
    httpRequest(HTTPMethods.POST, "/api/events/functions/create-" + service, requestParameters)
        .then(e => navigate("..", { relative: 'path' }))
        .catch((err) => {
          if (err.status === HttpStatusCode.Conflict) {
            setError("Функция с таким названием уже существует!")
          }
          setParameters(parameters)
          setIsProcessing(false)
        })
    setIsProcessing(true)
  }

  if (isProcessing)
    return <div className={styles.content}><span className={"loader dark"}></span></div>

  return (
      <div className={styles.content}>
        <div className={styles.newFunctionBox}>
          <h1>Новая функция</h1>
          <div className={styles.error}>{error}</div>
          <form onSubmit={handleSubmit}>
            <label>Название* </label>
            <input value={parameters.name || ""} maxLength={64} minLength={3}
                   onChange={e => handleOnChange("name", e.target.value)} required/>

            <label>Cервис* </label>
            <select value={service} onChange={e => setService(e.target.value)} required>
              <option value="">-- Выберите сервис --</option>
              <option value={"S3"}>Хранилище S3</option>
            </select>

            <ServiceParameters service={service} parameters={parameters} handleOnChange={handleOnChange}
                               handleCheckboxes={handleCheckboxes} />

            <label>Окружение* </label>
            <select value={parameters.environment || ""}
                    onChange={e => handleOnChange("environment", e.target.value)} required>
              <option value="">-- Выберите окружение --</option>
              <option value={"Python 3"}>Python 3</option>
            </select>

            <label>Путь к обработчику* </label>
            <input value={parameters.handlerPath || ""} maxLength={256} minLength={1} list={"handlers"}
                   onChange={e => handleOnChange("handlerPath", e.target.value)} required />
            <datalist id={"handlers"}>
              {projectStructure.filter(e => e[e.length - 1] !== "/")
                  .map(e => <option key={e} value={e} />)}
            </datalist>

            <label>Обработчик* </label>
            <input value={parameters.handler || ""} maxLength={256} minLength={1} list={"functions"}
                   onFocus={handleOnFonusRuns}
                   onChange={e => handleOnChange("handler", e.target.value)} required />
            <datalist id={"functions"}>
              {functionSuggestions.map(e => <option key={e} value={e} />)}
            </datalist>

            <label>Размер памяти* </label>
            <select value={parameters.memorySize || ""} defaultValue={""}
                    onChange={e => handleOnChange("memorySize", e.target.value)} required>
              <option value="">-- Размер памяти --</option>
              <option value={128}>128 МБ</option>
              <option value={256}>256 МБ</option>
              <option value={512}>512 МБ</option>
              <option value={1024}>1024 МБ</option>
            </select>

            <label>Таймаут (в секундах)* </label>
            <input value={parameters.timeout} type={"number"} max={300} min={1}
                   onChange={e => handleOnChange("timeout", e.target.value)} required/>

            <button type={"submit"}>Создать</button>
          </form>
        </div>
      </div>

  )
}

const ServiceParameters = ({service, parameters, handleOnChange, handleCheckboxes}) => {
  switch (service) {
    case "S3":
      return (
          <Fragment>
            <label className={styles.specialParameter}>Имя бакета* </label>
            <input value={parameters.bucket || ""} maxLength={64} minLength={3}
                   onChange={e => handleOnChange("bucket", e.target.value)} required/>

            <label className={styles.specialParameter}>Событие S3* </label>
            <div className={styles.checkboxes}>
              <label>
                <input checked={parameters?.events?.includes("s3:ObjectCreated:Put") || false} type={"checkbox"}
                       value={"s3:ObjectCreated:Put"}
                       onChange={e => handleCheckboxes("events", e.target.value, e.target.checked)}/> Загрузить объект
              </label>
              <label>
                <input checked={parameters?.events?.includes("s3:ObjectRemoved:Delete") || false} type={"checkbox"}
                       value={"s3:ObjectRemoved:Delete"}
                       onChange={e => handleCheckboxes("events", e.target.value, e.target.checked)}/> Удалить объект
              </label>
            </div>

            <label className={styles.specialParameter}>Префикс </label>
            <input value={parameters.prefix || ""} maxLength={256} onChange={e => handleOnChange("prefix", e.target.value)} />

            <label className={styles.specialParameter}>Суффикс </label>
            <input value={parameters.suffix || ""} maxLength={256} onChange={e => handleOnChange("suffix", e.target.value)}/>

          </Fragment>
      )
    default:
      return null
  }
}