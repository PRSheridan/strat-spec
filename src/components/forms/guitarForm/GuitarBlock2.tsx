import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const block2Schema = z
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

type Block2Data = z.infer<typeof block2Schema>

interface GuitarBlock2Props {
  onNext: (data: Block2Data) => void
}

function GuitarBlock2({ onNext }: GuitarBlock2Props) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<Block2Data>({
    resolver: zodResolver(block2Schema),
    defaultValues: {
      name: "",
      modified: false,
      modifications: "",
      description: "",
      images: [],
    },
  })

  function onSubmit(data: Block2Data) {
    console.log("Block 2 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 2: Personalization</h2>

        <div className="guitar-block-section">
          <label>Guitar Name</label>
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

export default GuitarBlock2

