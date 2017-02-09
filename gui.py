# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:42:37 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

# Import Buisness3D objects
from manufacture import Manufacture
from cost import costfunc1
from part import Order, Material, Part

# Import added modules 
from tkinter import Tk, Button, Text, END, filedialog


class Buisness3D:
    
    def __init__(self, master):
        self.master = master
        master.title("Buisness3D")
        
        self.setup()
        
        self.SetSTLs = Button(master, text="Add STL to Order", command=self.set_filename)
        self.SetSTLs.pack()
                
        self.SetSTLs = Button(master, text="Clear", command=self.clear_order)
        self.SetSTLs.pack()
        
        self.Partlisttext = Text(self.master,height=10, width=150)
        self.Partlisttext.pack()     

        self.CalcQuote = Button(master, text="Quote", command=self.calc_quote)
        self.CalcQuote.pack()        

        self.Quotelisttext = Text(self.master,height=10, width=150)
        self.Quotelisttext.pack()
        
        self.PrintQuote = Button(master, text="Print Quote", command=self.write_quote)
        self.PrintQuote.pack()  
        
    def setup(self):
        
        self.manufacture = Manufacture('MountMfg')
        self.manufacture.read()
        self.manufacture.calc_prop()
        

        # Set materials
        self.materials = {}
        
        mat = Material('VeroWhitePlus')
        mat.cost_g = 0.6 # $/g
        mat.density =0.00118 #g/mm^3 
        self.materials[mat.name] = mat
                      
        mat = Material('SUP705')
        mat.cost_g = 0.6 # $/g
        mat.density = 0.0009 #g/mm^3 
        self.materials[mat.name] = mat
                      
        # Initialize order
        self.order = Order()
        
    def clear_order(self):
        # Initialize order
        self.order = Order()
        
        
    def set_filename(self):
        filenames_str = filedialog.askopenfilenames(filetypes=[("*.STL","*.stl")])
        print ("filenames_str {0}".format(filenames_str))
        print ("Adding STL files:")
        for stl_file in list(filenames_str):
            print ("- {0} ".format(stl_file))
            part_name = stl_file.split("/")[-1].replace(".STL","")
            if( part_name in self.order.parts.keys() ):
                print ("!!!! Warning part already in order !!!!")
            item = Part(part_name)
            item.read_mesh(stl_file)
            item.calc_props()
            
            self.order.models[part_name] = item
        #print ("filenames {0}".format(filenames_str.splitlist()))
        
        self.write_stls()
        

        
    def write_stls(self):
        i=1
        
        #part_list = "Part list: \n"
        part_list = "Name ; Volume ; Size  :\n"       
        for  part_name,part in  self.order.parts.items():
            part_list += "{} ; {:.3f} ; {:.3f} x {:.2f} x {:.2f} \n".format(part_name \
                ,part.properties['Volume'] \
                ,part.properties['Size'][0] \
                ,part.properties['Size'][1] \
                ,part.properties['Size'][2] \
                          )
            i += 1
            
        self.Quotelisttext.delete(1.0,END)            
        self.Partlisttext.insert(END, part_list)
                
    def calc_quote(self):
        
        supmat = self.materials['SUP705']
        i=1
        packingslip_dic = {}
        packingslip_dic['ITEM #'] = []        
        packingslip_dic['DESCRIPTION'] = []
        packingslip_dic['QUANTITY'] = []
        
        
        quote_list = "Name ; Mass ; Item cost : \n"
        for  part_name,model in  self.order.models.items():
            mat = self.materials[model.material_name]
            model.set_manufacture(self.manufacture)
            model.set_mat(mat)
            
            model.set_supmat(supmat)
            model.estmiate_cost()
            quote_list += "{} ; {:.2f} ; {:.3f} \n".format(part_name, \
                           model.properties['Mass'],model.cost)
            # Add packing slip data frame information
            packingslip_dic['ITEM #'].append(i)
            packingslip_dic['DESCRIPTION'].append(part_name)
            packingslip_dic['QUANTITY'].append(model.qty)
            
            i += 1
            
        self.packingslip_df =    pd.DataFrame(packingslip_dic) 
        self.Quotelisttext.delete(1.0,END)
        self.Quotelisttext.insert(END, quote_list)
        
        
    def write_quote(self):
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('packingslip.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        self.packingslip_df[['ITEM #','DESCRIPTION','QUANTITY']].to_excel(writer, sheet_name='Packaging_Slip',index=False)
        worksheet = writer.sheets['Packaging_Slip']
                
        # Set the column width and format.
        worksheet.set_column('B:B', 60)
        worksheet.set_column('C:C', 10)
                             
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        
root = Tk()
Buisness3D_gui = Buisness3D(root)
root.mainloop()
        