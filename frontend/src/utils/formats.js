export const getStringDate = (time, includeMilliseconds) => {
  const date = new Date(time);

  let formatted = `${date.toLocaleDateString('ru-RU')} в ${date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })}`;

   if (includeMilliseconds) {
    const ms = String(date.getMilliseconds()).padStart(3, '0');
    formatted = `${formatted}.${ms}`;
  }

  return formatted;
}

export const getStringDateLog = (time) => {
  const date = new Date(time);

  let formatted = `${date.toLocaleDateString('ru-RU')} ${date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })}`;

  const ms = String(date.getMilliseconds()).padStart(3, '0');
  formatted = `${formatted}.${ms}`

  return formatted;
}
