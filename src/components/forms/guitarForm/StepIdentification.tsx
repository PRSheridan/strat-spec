import { useEffect, useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const identificationSchema = z
  .object({
    serial_number: z.string().min(3, "Serial number is required"),
    brand: z.string().min(1, "Brand is required"),
    custom_brand: z.string().optional(),
    model: z.string().nullable().optional(),
    serial_number_location: z.string().min(1, "Serial number location is required"),
    year: z
      .number()
      .min(1930, "Year must be at least 1930")
      .max(new Date().getFullYear(), "Year cannot be in the future")
      .nullable()
      .optional(),
    country: z.string().min(1, "Country is required"),
    custom_country: z.string().optional(),
  })
  .superRefine((data, ctx) => {
    if (data.brand === "not_listed" && !data.custom_brand?.trim()) {
      ctx.addIssue({
        path: ["custom_brand"],
        code: z.ZodIssueCode.custom,
        message: "Entry required if not already listed",
      })
    }

    if (data.country === "not_listed" && !data.custom_country?.trim()) {
      ctx.addIssue({
        path: ["custom_country"],
        code: z.ZodIssueCode.custom,
        message: "Entry required if not already listed",
      })
    }
  })

type IdentificationData = z.infer<typeof identificationSchema>

interface StepIdentificationProps {
  onNext: (data: IdentificationData) => void
}

function StepIdentification({ onNext }: StepIdentificationProps) {
  const [brandOptions, setBrandOptions] = useState<string[]>([])
  const [modelOptions, setModelOptions] = useState<{ id: string; name: string }[]>([])
  const [locationOptions, setLocationOptions] = useState<string[]>([])
  const [countryOptions, setCountryOptions] = useState<string[]>([])

  useEffect(() => {
    console.log("Errors:", errors)
    fetch("/api/identification-form")
      .then(res => res.json())
      .then(data => {
        console.log(data.brands)
        setBrandOptions(data.brands)
        setLocationOptions(data.serial_number_locations)
        setCountryOptions(data.countries)
      })
    fetch("/api/models")
      .then(res => res.json())
      .then(models => {
        setModelOptions(models.map((model: any) =>
          ({id: model.id, name: model.model_name})))
      }) 
  }, [])

  const { register, handleSubmit, watch, formState: { errors } } = useForm<IdentificationData>({
    resolver: zodResolver(identificationSchema),
    defaultValues: {
      serial_number: "",
      brand: "",
      custom_brand: "",
      model: null,
      serial_number_location: "",
      year: undefined,
      country: "",
      custom_country: "",
    },
  })

  function handleNext(data: IdentificationData) {
    const { brand, country, custom_brand, custom_country } = data
  
    if (brand === "not_listed" && custom_brand) {
      data.brand = custom_brand
    }
  
    if (country === "not_listed" && custom_country) {
      data.country = custom_country
    }
  
    if (data.custom_brand === "(ignore)") delete data.custom_brand
    if (data.custom_country === "(ignore)") delete data.custom_country
  
    console.log("Block 1 Data:", data)
    onNext(data)
  }
  

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(handleNext)}>
        <h2>Block 1: Identification</h2>

        <div className="guitar-block-section">
          <label>Serial Number*</label>
          <input {...register("serial_number")} placeholder="Enter serial number" />
          {errors.serial_number && <p>{errors.serial_number.message}</p>}
        </div>

        <div className="guitar-block-section">
          <label>Brand*</label>
          <select {...register("brand")}>
            <option value="">Select a Brand</option>
            <option value="">Unknown</option>
            <option value="not_listed">Not listed</option>
            {brandOptions.map((brand) => (
              <option key={brand} value={brand}>{brand}</option>
            ))}
          </select>
          {errors.brand && <p>{errors.brand.message}</p>}

          {watch("brand") === "not_listed" && (
            <>
              <input
                {...register("custom_brand")}
                placeholder="Enter your value"
              />
              {errors.custom_brand && <p>{errors.custom_brand.message}</p>}
            </>
          )}
        </div>

        <div className="guitar-block-section">
          <label>Model</label>
          <select {...register("model")}>
            <option value="">Select a Model</option>
            <option value="">Unknown / Not listed</option>
            {modelOptions.map((model) => (
              <option key={model.id} value={model.id}>{model.name}</option> //---------------------------------------------------------
            ))}
          </select>
        </div>

        <div className="guitar-block-section">
          <label>Serial Number Location*</label>
          <select {...register("serial_number_location")}>
            <option value="">Select Location</option>
            {locationOptions.map((location) => (
              <option key={location} value={location}>{location}</option>
            ))}
          </select>
          {errors.serial_number_location && <p>{errors.serial_number_location.message}</p>}
        </div>

        <div className="guitar-block-section">
          <label>Year</label>
          <input type="number" {...register("year", { valueAsNumber: true })} placeholder="Enter year" />
          {errors.year && <p>{errors.year.message}</p>}
        </div>

        <div className="guitar-block-section">
          <label>Country*</label>
          <select {...register("country")}>
            <option value="">Select a Country</option>
            <option value="not_listed">Not listed</option>
            {countryOptions.map((country) => (
              <option key={country} value={country}>{country}</option>
            ))}
          </select>
          {errors.country && <p>{errors.country.message}</p>}

          {watch("country") === "not_listed" && (
            <>
              <input
                {...register("custom_country")}
                placeholder="Enter your value"
              />
              {errors.custom_country && <p>{errors.custom_country.message}</p>}
            </>
          )}
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default StepIdentification
