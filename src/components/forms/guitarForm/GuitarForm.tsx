import { useState } from "react";
import { useNavigate } from "react-router-dom"
import "./guitarForm.css"
import StepInformation from "./StepInformation"
import StepIdentification from "./StepIdentification"
import StepPhysicalSpecs from "./StepPhyscialSpecs"
import StepBodySpecs from "./StepBodySpecs"
import StepNeckSpecs from "./StepNeckSpecs"
import StepElectronics from "./StepElectronics"
import StepPersonalization from "./StepPersonalization"

export const steps = [
  {
    id: 0,
    name: "Information",
    component: StepInformation
  },
  {
    id: 1,
    name: "Identification",
    component: StepIdentification
  },
  {
    id: 2,
    name: "Physical Specs",
    component: StepPhysicalSpecs
  },
  {
    id: 3,
    name: "Body Specs",
    component: StepBodySpecs
  },
  {
    id: 4,
    name: "Neck Specs",
    component: StepNeckSpecs
  },
  {
    id: 5,
    name: "Electronics",
    component: StepElectronics
  },
  {
    id: 6,
    name: "Personalization",
    component: StepPersonalization
  }
]

export default function GuitarForm() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [formData, setFormData] = useState({})

  function handleNext(data: any) {
    setFormData((prev) => ({ ...prev, ...data }))
    setStep((prev) => prev + 1)
    console.log(step + 1)
    console.log("Current Form Data", formData)
  }

  const StepComponent = steps[step].component
  return <StepComponent onNext={handleNext} />
}
