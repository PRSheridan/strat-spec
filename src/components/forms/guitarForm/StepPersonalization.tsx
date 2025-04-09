import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const personalizationSchema = z
  .object({
    name: z.string().min(3, "Guitar name must be at least 3 characters"),
    modified: z.boolean().nullable().optional(),
    modifications: z.string().nullable().optional(),
    description: z.string().nullable().optional(),
    images: z.array(z.instanceof(File)).nullable().optional(),
  })
  .refine((data) => {
    if (data.modified && (!data.modifications || data.modifications.trim().length === 0)) {
      return false
    }
    return true
  }, {
    message: "Please describe the modifications",
    path: ["modifications"],
  })

type PersonalizationData = z.infer<typeof personalizationSchema>

interface StepPersonalizationProps {
  onNext: (data: PersonalizationData) => void
}

function StepPersonalization({ onNext }: StepPersonalizationProps) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<PersonalizationData>({
    resolver: zodResolver(personalizationSchema),
    defaultValues: {
      name: "",
      modified: false,
      modifications: "",
      description: "",
      images: [],
    },
  })

  function onSubmit(data: PersonalizationData) {
    console.log("Step 6 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Step 6: Personalization</h2>

        <div className="guitar-block-section">
          <label>Guitar Name</label>
          <div>year country Brand Stratocaster (modified)</div>
          <input {...register("name")} placeholder="Enter guitar name" />
          {errors.name && <p>{errors.name.message}</p>}
        </div>

        <div className="guitar-block-section inline">
          <label>Modified?</label>
          <label className="guitar-switch">
            <input type="checkbox" {...register("modified")} />
            <span className="guitar-slider" />
          </label>
        </div>

        {watch("modified") && (
          <div className="guitar-block-section">
            <label>Modifications</label>
            <textarea {...register("modifications")} placeholder="Describe modifications" />
            {errors.modifications && <p>{errors.modifications.message}</p>}
          </div>
        )}

        <div className="guitar-block-section">
          <label>Description (Optional)</label>
          <textarea {...register("description")} placeholder="Enter guitar description" />
        </div>

        <div className="guitar-block-section">
          <label>Upload Images</label>
          <input
            type="file"
            multiple
            onChange={(e) => {
              setValue("images", Array.from(e.target.files || []))
            }}
          />
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default StepPersonalization


