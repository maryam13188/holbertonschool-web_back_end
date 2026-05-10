/**
 * Executes a math function and records its result or error in a queue.
 * @param {Function} mathFunction - The function to be executed.
 * @returns {Array} A queue containing the result/error and a completion message.
 */
export default function guardrail(mathFunction) {
  const queue = [];

  try {
    // محاولة تنفيذ الدالة وإضافة النتيجة للمصفوفة
    const result = mathFunction();
    queue.push(result);
  } catch (error) {
    // في حال حدوث خطأ، نقوم بإضافة رسالة الخطأ كنص
    queue.push(String(error));
  } finally {
    // يتم تنفيذ هذا الجزء دائماً سواء نجحت الدالة أو فشلت
    queue.push('Guardrail was processed');
  }

  return queue;
}
