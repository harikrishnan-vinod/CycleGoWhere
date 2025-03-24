import { useState } from "react";

export function useForm<T>(initialValues: T) {
  const [form, setForm] = useState<T>(initialValues);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  return { form, handleChange, setForm };
}
