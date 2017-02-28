# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:42:37 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

# Import Buisness3D objects
from manufacture import Manufacture, PrinterTray
import cost
from part import Order, Material, Part
import pandas as pd
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
        mat.cost_g = 1.6 # $/g
        mat.density = 1.18/1000.0 #g/mm^3 
        self.materials[mat.name] = mat
                      
        mat = Material('SUP705')
        mat.cost_g = 0.6 # $/g
        mat.density = 1.17/1000.0 #g/mm^3 
        self.materials[mat.name] = mat
                      
        # Initialize order
        self.clear_order()
        
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
            part = Part(part_name)
            part.read_mesh(stl_file)
            part.calc_props()
            
            self.order.parts[part_name] = part
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
        
        mat = self.materials['VeroWhitePlus']
        supmat = self.materials['SUP705']
        i=1
        packingslip_dic = {}
        packingslip_dic['ITEM #'] = []        
        packingslip_dic['DESCRIPTION'] = []
        packingslip_dic['QUANTITY'] = []
        
        
        quote_list = "Name ; Mass ; Item cost : \n"
        for  part_name,part in  self.order.parts.items():
            part.calc_mass(mat)
            
            suportheight = 1.5
            
            tray = PrinterTray('OBJET')
            tray.properties['MAX_X'] = 200.0
            tray.properties['MAX_Y'] = 240.0

            part.cost = cost.costfunc1(tray.properties['MAX_X'] \
                                        ,tray.properties['MAX_Y'] \
             ,part.properties['Height'] \
             ,part.properties['Size'][0] \
             ,part.properties['Size'][1] \
             ,part.properties['Size'][2] \
             ,mat.cost_g \
             ,part.properties['Mass'] \
             ,supmat.cost_g \
             ,supmat.density \
             ,part.properties['SrufArea']*suportheight \
             ,part.qty \
              ,self.manufacture.properties['target_income'] \
             ,self.manufacture.properties['operating_days'] \
             ,self.manufacture.properties['operating_hours'] \
             ,self.manufacture.properties['z_base_height'] \
             ,self.manufacture.properties['seconds_per_layer'] \
             ,self.manufacture.properties['max_quantity_discount'] \
             ,self.manufacture.properties['discount_per_part'] \
             )          
            
            quote_list += "{} ; {:.2f} ; {:.3f} \n".format(part_name, \
                           part.properties['Mass'],part.cost)
            # Add packing slip data frame information
            packingslip_dic['ITEM #'].append(i)
            packingslip_dic['DESCRIPTION'].append(part_name)
            packingslip_dic['QUANTITY'].append(part.qty)
            
            i += 1
            
        self.packingslip_df =  pd.DataFrame(packingslip_dic) 
        self.Quotelisttext.delete(1.0,END)
        self.Quotelisttext.insert(END, quote_list)
        
        
    def write_quote(self):
        pslip_f = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                        ("All files", "*.*") ))
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('{}.xlsx'.format(pslip_f), engine='xlsxwriter')

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
        