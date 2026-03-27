const padFormatted = (str) => String(str).padStart(2, '0')

export const getStringDate = (unixTime, includeMilliSeconds) => {
  const unixDate = new Date(unixTime)

  const date = {
    day: padFormatted(unixDate.getDate()),
    month: padFormatted(unixDate.getMonth()),
    year: padFormatted(unixDate.getFullYear()),
    hour: padFormatted(unixDate.getHours()),
    minutes: padFormatted(unixDate.getMinutes()),
    seconds: padFormatted(unixDate.getSeconds()),
    milliseconds: padFormatted(unixDate.getMilliseconds())
  }
  return `${date.day}.${date.month}.${date.year} в ${date.hour}:${date.minutes}:${date.seconds}` +
          `${includeMilliSeconds ? ":" + date.milliseconds : ""}`
}