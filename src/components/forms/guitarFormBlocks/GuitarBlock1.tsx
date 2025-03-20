import { useEffect, useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Model } from "../../../types"

// Validation Schema
const block1Schema = z.object({
  serial_number: z.string().min(3, "Serial number is required"),
  brand: z.string().min(1, "Brand is required"),
  model: z.string().nullable(), // Model can be selected or left empty
  serial_number_location: z.string().min(1, "Serial number location is required"),
  year: z.number().min(1930, "Year must be at least 1930").max(new Date().getFullYear(), "Year cannot be in the future").optional(),
  country: z.string().min(1, "Country is required"),
})

type Block1Data = z.infer<typeof block1Schema>

interface GuitarBlock1Props {
  onNext: (data: Block1Data) => void
}

function GuitarBlock1({ onNext }: GuitarBlock1Props) {
  const [brandOptions, setBrandOptions] = useState<string[]>([])
  const [modelOptions, setModelOptions] = useState<{ id: string; name: string }[]>([])
  const [locationOptions, setLocationOptions] = useState<string[]>([])
  const [countryOptions, setCountryOptions] = useState<string[]>([])

  useEffect(() => {
    fetch("/api/brands").then(res => res.json()).then(setBrandOptions)
    fetch("/api/models").then(res => res.json()).then(models => setModelOptions(models.map((model: any) => ({id: model.id, name: model.model_name}))))
    fetch("/api/serial-number-locations").then(res => res.json()).then(setLocationOptions)
    fetch("/api/countries").then(res => res.json()).then(setCountryOptions)
  }, [])

  const { register, handleSubmit, formState: { errors } } = useForm<Block1Data>({
    resolver: zodResolver(block1Schema),
    defaultValues: {
      serial_number: "",
      brand: "",
      model: null,
      serial_number_location: "",
      year: undefined,
      country: "",
    },
  })

  const onSubmit = (data: Block1Data) => {
    console.log("Block 1 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 1: Identification</h2>

        <div>
          <label>Serial Number</label>
          <input {...register("serial_number")} placeholder="Enter serial number" />
          {errors.serial_number && <p>{errors.serial_number.message}</p>}
        </div>

        <div>
          <label>Brand</label>
          <select {...register("brand")}>
            <option value="">Select a Brand</option>
            {brandOptions.map((brand) => (
              <option key={brand} value={brand}>{brand}</option>
            ))}
          </select>
          {errors.brand && <p>{errors.brand.message}</p>}
        </div>

        <div>
          <label>Model (Optional)</label>
          <select {...register("model")}>
            <option value="">Select a Model</option>
            {modelOptions.map((model) => (
              <option key={model.id} value={model.id}>{model.name}</option> //---------------------------------------------------------
            ))}
          </select>
        </div>

        <div>
          <label>Serial Number Location</label>
          <select {...register("serial_number_location")}>
            <option value="">Select Location</option>
            {locationOptions.map((location) => (
              <option key={location} value={location}>{location}</option>
            ))}
          </select>
          {errors.serial_number_location && <p>{errors.serial_number_location.message}</p>}
        </div>

        <div>
          <label>Year</label>
          <input type="number" {...register("year", { valueAsNumber: true })} placeholder="Enter year" />
          {errors.year && <p>{errors.year.message}</p>}
        </div>

        <div>
          <label>Country</label>
          <select {...register("country")}>
            <option value="">Select a Country</option>
            {countryOptions.map((country) => (
              <option key={country} value={country}>{country}</option>
            ))}
          </select>
          {errors.country && <p>{errors.country.message}</p>}
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default GuitarBlock1
