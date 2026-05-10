/**
 * Returns a Promise.
 * @returns {Promise} A new promise object.
 */
export default function getResponseFromAPI() {
  return new Promise((resolve) => {
    /*
     * في هذه المهمة، المطلوب فقط إرجاع الوعد (Promise).
     * يمكننا استدعاء resolve() لجعله مكتملًا إذا لزم الأمر،
     * لكن الاختبار هنا يتحقق فقط من نوع الكائن (instanceof Promise).
     */
    resolve();
  });
}
