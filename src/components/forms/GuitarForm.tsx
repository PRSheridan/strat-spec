import { useState } from "react";
import { useNavigate } from "react-router-dom";
import GuitarBlock1 from "./guitarFormBlocks/GuitarBlock1";
import GuitarBlock2 from "./guitarFormBlocks/GuitarBlock2";

export default function GuitarForm() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({}); // Store all form data

  // Function to save Block 1 data and move forward
  const handleNext = (data: any) => {
    setFormData((prev) => ({ ...prev, ...data })); // Merge previous data
    setStep(step + 1); // Move to next step
    console.log(data)
  }

  return (
    <div id="guitar-form">
      {step === 0 && <GuitarBlock1 onNext={handleNext} />}
      {step === 1 && <GuitarBlock2 onNext={handleNext} />}
    </div>
  )
}
