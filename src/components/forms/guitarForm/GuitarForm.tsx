import { useState } from "react";
import { useNavigate } from "react-router-dom";
import GuitarBlockInfo from "./GuitarBlockInfo";
import GuitarBlock1 from "./GuitarBlock1";
import GuitarBlock2 from "./GuitarBlock2";
import GuitarBlock3 from "./GuitarBlock3";
import "./guitarForm.css"

export default function GuitarForm() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [formData, setFormData] = useState({})

  // When onNext is called on each form block, data is merged and step is increased
  function handleNext(data: any) {
    setFormData((prev) => ({ ...prev, ...data }))
    setStep(step + 1)
    console.log(formData)
  }

  return (
    <div id="guitar-form">
      {step === 0 && <GuitarBlockInfo onNext={handleNext} />}
      {step === 1 && <GuitarBlock1 onNext={handleNext} />}
      {step === 2 && <GuitarBlock2 onNext={handleNext} />}
      {step === 3 && <GuitarBlock3 onNext={handleNext} />}
    </div>
  )
}
