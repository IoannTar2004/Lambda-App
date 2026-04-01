const padFormatted = (str) => String(str).padStart(2, '0')

export const getStringDate = (isoString, includeMilliSeconds) => {
  const date = new Date(isoString);

  const formatted = `${date.toLocaleDateString('ru-RU')} в ${date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })}`;

  return formatted;
}